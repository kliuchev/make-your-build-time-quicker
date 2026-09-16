// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "Feature14Data",
    products: [.library(name: "Feature14Data", targets: ["Feature14Data"])],
    dependencies: [.package(path: "../Feature14Domain")],
    targets: [.target(name: "Feature14Data", dependencies: [.product(name: "Feature14Domain", package: "Feature14Domain")])]
)
