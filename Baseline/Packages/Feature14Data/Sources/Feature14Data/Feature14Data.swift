import Feature14Domain

public enum Feature14DataRepository {
    public static func load(_ id: Int) -> Feature14DomainModel {
        Feature14DomainModel(id: id, title: "Feature 14")
    }
}
