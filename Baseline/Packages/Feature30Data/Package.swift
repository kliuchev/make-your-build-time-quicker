// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature30Data",
    products: [.library(name: "Feature30Data", targets: ["Feature30Data"])],
    dependencies: [.package(path: "../Feature30Domain")],
    targets: [.target(name: "Feature30Data", dependencies: [.product(name: "Feature30Domain", package: "Feature30Domain")])]
)
