// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature11Data",
    products: [.library(name: "Feature11Data", targets: ["Feature11Data"])],
    dependencies: [.package(path: "../Feature11Domain")],
    targets: [.target(name: "Feature11Data", dependencies: [.product(name: "Feature11Domain", package: "Feature11Domain")])]
)
