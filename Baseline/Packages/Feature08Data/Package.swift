// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature08Data",
    products: [.library(name: "Feature08Data", targets: ["Feature08Data"])],
    dependencies: [.package(path: "../Feature08Domain")],
    targets: [.target(name: "Feature08Data", dependencies: [.product(name: "Feature08Domain", package: "Feature08Domain")])]
)
